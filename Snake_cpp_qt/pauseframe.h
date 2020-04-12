#ifndef PAUSEFRAME_H
#define PAUSEFRAME_H

#include <QWidget>
#include <QFrame>
#include <QPushButton>
#include <QPainter>
#include <QLabel>

class PauseFrame : public QFrame {
    Q_OBJECT

public:
    PauseFrame(QWidget *parent = nullptr);
    ~PauseFrame();

private slots:
    void paintEvent(QPaintEvent *event);

private:
    QPushButton *bto_main_menu, *bexit;
    QLabel *menu_text;
};

#endif // PAUSEFRAME_H
