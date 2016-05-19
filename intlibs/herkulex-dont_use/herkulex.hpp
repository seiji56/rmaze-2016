#include <vector>
#include <wiringSerial.h>
#include <wiringPi.h>
#include <unistd.h>
#include <time.h>

#include <stdio.h>


enum h_command
{
    EEP_WRITE = 0x01,
    EEP_READ  = 0x02,
    RAM_WRITE = 0x03,
    RAM_READ  = 0x04,
    I_JOG     = 0x05,
    S_JOG     = 0x06,
    STAT      = 0x07,
    ROLLBACK  = 0x08,
    REBOOT    = 0x09
};

enum h_eep_addr
{
    EEPMODEL_N1    = 0x00,
    EEPMODEL_N2    = 0x01,
    EEPVERSION1    = 0x02,
    EEPVERSION2    = 0x03,
    EEPBAUD_RATE   = 0x04,
    EEPID          = 0x06,
    EEPACK_POLICY  = 0x07,
    EEPALARM_LED   = 0x08,
    EEPTORQUE_POL  = 0x09,
    EEPMAX_TEMP    = 0x0B,
    EEPMIN_VOLTAGE = 0x0C,
    EEPMAX_VOLTAGE = 0x0D,
    EEPACCEL_RATIO = 0x0E,
    EEPACCEL_TIME  = 0x0F,
    EEPDEAD_ZONE   = 0x10,
    EEPSAT_OFFSET  = 0x11,
    EEPSAT_SLOPE   = 0x12,
    EEPPWM_OFFSET  = 0x14,
    EEPMIN_PWM     = 0x15,
    EEPMAX_PWM     = 0x16,
    EEPOVER_PWM    = 0x18,
    EEPMIN_POS     = 0x1A,
    EEPMAX_POS     = 0x1C,
    EEPPOS_KP      = 0x1E,
    EEPPOS_KD      = 0x20,
    EEPPOS_KI      = 0x22,
    EEPPOS_FF_1STG = 0x24,
    EEPPOS_FF_2STG = 0x26,
    EEPLED_BLINK   = 0x2C,
    EEPADC_FAULT   = 0x2D,
    EEPPACK_GARB   = 0x2E,
    EEPSTOP_DET    = 0x2F,
    EEPOVER_DET    = 0x30,
    EEPSTOP_STHRE  = 0x31,
    EEPIMP_MARGIN  = 0x32,
    EEPCALIB_DIF   = 0x35
};

enum h_ram_addr
{
    RAMID          = 0x00,
    RAMACK_POLICY  = 0x01,
    RAMALARM_LED   = 0x02,
    RAMTORQUE_POL  = 0x03,
    RAMMAX_TEMP    = 0x05,
    RAMMIN_VOLTAGE = 0x06,
    RAMMAX_VOLTAGE = 0x07,
    RAMACCEL_RATIO = 0x08,
    RAMACCEL_TIME  = 0x09,
    RAMDEAD_ZONE   = 0x0A,
    RAMSAT_OFFSET  = 0x0B,
    RAMSAT_SLOPE   = 0x0C,
    RAMPWM_OFFSET  = 0x0E,
    RAMMIN_PWM     = 0x0F,
    RAMMAX_PWM     = 0x10,
    RAMOVER_PWM    = 0x12,
    RAMMIN_POS     = 0x14,
    RAMMAX_POS     = 0x16,
    RAMPOS_KP      = 0x18,
    RAMPOS_KD      = 0x1A,
    RAMPOS_KI      = 0x1C,
    RAMPOS_FF_1STG = 0x1E,
    RAMPOS_FF_2STG = 0x20,
    RAMLED_BLINK   = 0x26,
    RAMADC_FAULT   = 0x27,
    RAMPACK_GARB   = 0x28,
    RAMSTOP_DET    = 0x29,
    RAMOVER_DET    = 0x2A,
    RAMSTOP_STHRE  = 0x2B,
    RAMIMP_MARGIN  = 0x2C,
    RAMCALIB_DIF   = 0x2F,
    RAMSTAT_ERR    = 0x30,
    RAMSTAT_DETAIL = 0x31,
    RAMTORQUE_CONT = 0x34,
    RAMLED_CONTROL = 0x35,
    RAMVOLTAGE     = 0x36,
    RAMTEMPERATURE = 0x37,
    RAMCURR_CON_M  = 0x38,
    RAMTICK        = 0x39,
    RAMCALIB_POS   = 0x3A,
    RAMABSOL_POS   = 0x3C,
    RAMDIFF_POS    = 0x3E,
    RAMPWM         = 0x40,
    RAMABS_GOAL    = 0x42,
    RAMABS_DES_TR  = 0x44,
    RAMDESIRED_V   = 0x46
};

enum h_color
{
    none   = -1,
    black  = 0,
    green  = 1,
    blue   = 2,
    cyan   = 3,
    red    = 4, 
    what   = 5,
    purple = 6
};

//H_PKT

class h_pkt
{
public:
    h_pkt();
    h_pkt(int _size, int _pid, int _cmd);
    
    void setsize(int _size);
    void setpid(int _pid);
    void setcmd(int _cmd);
    void setdata(char* _data, int sz);
    
    char getsize();
    char getpid();
    char getcmd();
    char* getdata();
    
    void calcchk();
    
protected:
    char header1;
    char header2;
    char size;
    char pID;
    char CMD;
    char chk1;
    char chk2;
    char data[256];
};

//EEP_READ
class h_eepread : public h_pkt
{
public:
    h_eepread();
    h_eepread(int _pID, int addr, int length);
    
    void setsize(int _size);
    void setcmd(int _cmd);
};
//EEP_WRITE
class h_eepwrite : public h_pkt
{
public:
    h_eepwrite();
    h_eepwrite(int _pID, int addr, int length, char* _data);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setaddress(int addr);
    void setlength(int length);
    void setdata(char* _data, int sz);
};
//RAM_READ
class h_ramread : public h_pkt
{
public:
    h_ramread();
    h_ramread(int _pID, int addr, int length);
    
    void setsize(int _size);
    void setcmd(int _cmd);
};
//RAM_WRITE
class h_ramwrite : public h_pkt
{
public:
    h_ramwrite();
    h_ramwrite(int _pID, int addr, int length, char* _data);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setaddress(int addr);
    void setlength(int length);
    void setdata(char* _data, int sz);
};

//I_JOG
class h_ijog : public h_pkt
{
public:
    h_ijog();
    h_ijog(int _pID);
    
    void addmot(int _pid, int pot, int SET, int time);
    bool hasmot(int _pid);
    void remmot(int _pid);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setdata(char* _data, int sz);
private:
    int mcnt;
};

//S_JOG
class h_sjog : public h_pkt
{
public:
    h_sjog();
    h_sjog(int _pID);
    
    void addmot(int _pid, int pot, int SET);
    bool hasmot(int _pid);
    void remmot(int _pid);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setdata(char* _data, int sz);
    void settime(int time);
private:
    int mcnt;
};

//STAT
class h_stat : public h_pkt
{
public:
    h_stat();
    h_stat(int _pID);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setdata(char* _data, int sz);
};

//ROLLBACK
class h_rollback : public h_pkt
{
public:
    h_rollback();
    h_rollback(int _pID, bool idskip, bool bandskip);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setdata(char* _data, int sz);
    
    void setidskip(int idskip);
    void setbandskip(int bandskip);
};

//REBOOT
class h_reboot : public h_pkt
{
public:
    h_reboot();
    h_reboot(int _pID);
    
    void setsize(int _size);
    void setcmd(int _cmd);
    void setdata(char* _data, int sz);
};

//MOTOR
struct h_motor
{
public:
    h_motor();
    h_motor(int _pID, bool inverted, float _calib);
    
    int pID;
    bool inv;
    float calib;
};

//HERKULEX CHAIN CONTROLLER

class herkulex_chain
{
public:
    herkulex_chain(char* s_port, int baud);
    
    void writeeep(int addr, int size, char* data, int id);
    void readeep(int addr, int size, char* data, int id, int tout);
    
    void writeram(int addr, int size, char* data, int id);
    void readram(int addr, int size, char* data, int id, int tout);
    
    void setcolor(h_color color, int id);
    void setspeed(int speed, h_color color, int id);
    void setpos  (int pos, h_color color, int id);
    
    void clearerr(h_color color, int id);
    
    void addmot(int _pid, bool inv, float calib);
    bool hasmot(int _pid);
    void remmot(int _pid);
private:
    void sendp(h_pkt &packet);
    void readp(h_pkt &packet, unsigned int timeout);
    
    int serial_fd;
    
    std::vector<h_motor> motors;
};
