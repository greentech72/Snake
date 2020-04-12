#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow) {
    ui->setupUi(this);
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::moveUP(){
    snake[0].direction = 'u';
}

void MainWindow::moveDOWN(){
    snake[0].direction = 'd';
}

void MainWindow::moveRIGHT(){
    snake[0].direction = 'r';
}

void MainWindow::moveLEFT(){
    snake[0].direction = 'l';
}

void MainWindow::addScore(){
    SCORE += 10;
    auto seg = *(snake.end() - 1);
    seg.direction = '0';
    snake.push_back(seg);
    apple.re();
}

void MainWindow::pause(){
    if(GAME_STATUS != 'p'){
        GAME_STATUS = 'p';
        pf = new PauseFrame(this);
        pf->show();
    }
    else{
        GAME_STATUS = 'g';
        delete pf;
        //mainMenu();
    }
}

void MainWindow::mainMenu(){
    GAME_STATUS = 's';
    delete left;
    delete right;
    delete up;
    delete down;
    delete pause_shortcut;
    if(GAME_STATUS != 'd')
        delete pf;
    snake.clear();
    game_init_zed = false;
    SCORE = 30;

    ui->pBExit->show();
    ui->pBStart->show();
    setMaximumSize(QSize(400, 500));
    setMinimumSize(QSize(400, 500));
    resize(400, 500);
    update();
}

void MainWindow::DEFEAT(){
    GAME_STATUS = 'd';
    QTimer::singleShot(1000, this, SLOT(mainMenu()));
    update();
}

void MainWindow::paintEvent(QPaintEvent *event){
    if(GAME_STATUS == 'g' || GAME_STATUS == 'p'){
    QPainter painter(this);
    painter.fillRect(0, 0, 500, 500, QBrush(QColor(42, 250, 84)));
    painter.setPen(QColor(0, 0, 0));
#ifdef DEBUG
    for(int i = 0; i < 25; i++){
        painter.drawLine( i * 20, 0, i * 20, height());
        painter.drawLine( 0, i * 20, width(), i * 20);
    }
#endif
    painter.setBrush(QBrush(QColor(23, 12, 173)));

        if(!game_init_zed){

            // INIT. SHORTCUTS (MOVEMENT)
            up = new QShortcut(QKeySequence("w"), this);
            connect(up, SIGNAL(activated()), this, SLOT(moveUP()));
            down = new QShortcut(QKeySequence("s"), this);
            connect(down, SIGNAL(activated()), this, SLOT(moveDOWN()));
            right = new QShortcut(QKeySequence("d"), this);
            connect(right, SIGNAL(activated()), this, SLOT(moveRIGHT()));
            left = new QShortcut(QKeySequence("a"), this);
            connect(left, SIGNAL(activated()), this, SLOT(moveLEFT()));
            pause_shortcut = new QShortcut(QKeySequence("escape"), this);
            connect(pause_shortcut, SIGNAL(activated()), this, SLOT(pause()));

            // CREATE SNAKE WITH 3 ELEMENTS
            segment head;
            head.pos = QPoint(10, 10);
            head.direction = 'd';
            snake.push_back(head);
            snake.push_back(segment(QPoint(11, 10), 'l'));
            snake.push_back(segment(QPoint(12, 10), 'l'));
            snake.push_back(segment(QPoint(13, 10), 'l'));

            // DRAW SNAKE
            for(auto seg: snake){
                auto p = seg.pos;
                painter.drawEllipse(p.x() * 20, p.y() * 20,
                                    20, 20);
            }

            // SET TIMER
            QTimer::singleShot(100, this, SLOT(update()));
            game_init_zed = true;
            return;
        }

        // CHECK APPLE
        if(apple.pos == snake[0].pos){
            addScore();
        }

        // MOVE
        char prevd = '0', d;
        for(segment &seg: snake){
            if(seg.direction == 'r'){
                seg.pos.setX(seg.pos.x() + 1);
            }
            else if(seg.direction == 'l'){
                seg.pos.setX(seg.pos.x() - 1);
            }
            else if(seg.direction == 'u'){
                seg.pos.setY(seg.pos.y() - 1);
            }
            else if(seg.direction == 'd'){
                seg.pos.setY(seg.pos.y() + 1);
            }

            d = seg.direction;
            if(prevd != '0'){
                seg.direction = prevd;
            }
            prevd = d;
        }

        // BORDERS IS FINE
        if(!DEFEAT_BY_BORDER){
            for(segment &seg: snake){
                if(seg.pos.x() >= 25){
                    seg.pos.setX(0);
                }
                else if(seg.pos.x() < 0){
                    seg.pos.setX(25);
                }

                if(seg.pos.y() >= 25){
                    seg.pos.setY(0);
                }
                else if(seg.pos.y() < 0){
                    seg.pos.setY(25);
                }
            }
        }

        // CHECK DEATH
        // BY SELF EATING
        for(int i = 1; i < snake.size(); i++){
            segment seg = snake[i];
            if(seg.pos == snake[0].pos){
                DEFEAT();
            }
        }

        // BY BORDERS
        if(DEFEAT_BY_BORDER){

        }

        // PAINT
        for(auto seg: snake){
            auto p = seg.pos;
            painter.drawEllipse(p.x() * 20, p.y() * 20,
                                20, 20);
        }

        painter.setBrush(QBrush(QColor(252, 3, 65)));
        painter.drawEllipse(apple.pos.x() * 20, apple.pos.y() * 20, 20, 20);

        // SET TIMER
        if(GAME_STATUS == 'g'){
            QTimer::singleShot(100, this, SLOT(update()));
        }
    }
    else if(GAME_STATUS == 'd'){
        QPainter painter(this);
        painter.setPen(QColor(255, 0, 0));
        painter.drawText(QPoint(width() / 2 - 50, height() / 2), "DEFEAT");
    }
    else{
        QPainter painter(this);
        painter.fillRect(0, 0, width(), height(), QBrush(QColor(255, 255, 255)));
    }
}

void MainWindow::on_pBStart_clicked() {
    setMaximumSize(QSize(500, 500));
    setMinimumSize(QSize(500, 500));
    ui->pBExit->hide();
    ui->pBStart->hide();
    GAME_STATUS = 'g';
    update();
}
