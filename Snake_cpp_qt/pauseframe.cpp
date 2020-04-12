#include "pauseframe.h"

PauseFrame::PauseFrame(QWidget *parent)
    : QFrame(parent) {

    setGeometry(parent->width() / 2 - 88, parent->height() / 2 - 88, 176, 150);

    menu_text = new QLabel(this);
    menu_text->setText("Menu");
    menu_text->setFont(parent->font());
    menu_text->move(50, 5);
    menu_text->show();

    bto_main_menu = new QPushButton(this);
    bto_main_menu->setText("To Main Menu");
    bto_main_menu->move(0, 50);
    bto_main_menu->setFont(parent->font());
    bto_main_menu->show();
    bto_main_menu->resize(176, bto_main_menu->height());
    connect(bto_main_menu, SIGNAL(clicked()), parent, SLOT(mainMenu()));

    bexit = new QPushButton(this);
    bexit->setText("Exit");
    bexit->move(0, bto_main_menu->pos().y() + 50);
    bexit->setFont(parent->font());
    bexit->resize(bto_main_menu->size());
    bexit->show();
    bexit->resize(176, bexit->height());
    connect(bexit, SIGNAL(clicked()), parent, SLOT(close()));

}

void PauseFrame::paintEvent(QPaintEvent *event){
    QPainter painter(this);
    painter.fillRect(0, 0, width(), height(), QBrush(QColor(114, 252, 213, 200)));
}

PauseFrame::~PauseFrame(){

}

