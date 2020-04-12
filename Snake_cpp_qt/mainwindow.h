#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QPainter>
#include <QVector>
#include <QTimer>
#include <QShortcut>
#include <QFrame>

#include <random>

#include "pauseframe.h"

//#define DEBUG

struct segment{
    QPoint pos;
    char direction;
    segment(QPoint p, char d){
        pos = p;
        direction = d;
    }
    segment(){

    }
};

struct apple_type{
    QPoint pos;

    apple_type(){
        re();
    }

    void re(){
        pos = QPoint(rand() % 25, rand() % 25);
    }
};

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pBStart_clicked();
    void paintEvent(QPaintEvent *event);
    void moveUP();
    void moveDOWN();
    void moveRIGHT();
    void moveLEFT();
    void pause();

    void mainMenu();

private:
    void addScore();
    void DEFEAT();

    char GAME_STATUS = 's'; // g - go, p - pause, s - stop, d - DEFEAT
    bool game_init_zed = false;
    bool DEFEAT_BY_BORDER = false;
    int SCORE = 30;
    QVector<segment> snake;
    Ui::MainWindow *ui;
    apple_type apple;
    QShortcut *up, *down, *left, *right, *pause_shortcut;
    PauseFrame *pf;

};
#endif // MAINWINDOW_H
