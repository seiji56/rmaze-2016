#include "herkulex.hpp"

//h_pkt definitions

h_pkt::h_pkt() : header1(0xFF), header2(0xFF), size(7)
{
    calcchk();
}

h_pkt::h_pkt(int _size, int _pid, int _cmd) : header1(0xFF), header2(0xFF), size(_size), pID(_pid), CMD(_cmd)
{
    calcchk();
}

void h_pkt::calcchk()
{
    chk1 = size;
    chk1 ^= pID;
    chk1 ^= CMD;
    for (int i = 0; i < size-7; i++)
    {
        chk1 ^= data[i];
    }
        
    chk1 &= 0xFE;
   
    chk2 = (~chk1)&0xFE;
}

//setter

void h_pkt::setsize(int _size)
{
    size = _size;
    calcchk();
}

void h_pkt::setpid(int _pid)
{
    pID = _pid;
    calcchk();
}

void h_pkt::setcmd(int _cmd)
{
    CMD = _cmd;
    calcchk();
}

void h_pkt::setdata(char* _data, int sz)
{
    for (int i = 0; i < sz; i++) data[i] = _data[i];
    calcchk();
}

char h_pkt::getsize()
{
    return size;
}

char h_pkt::getpid()
{
    return pID;
}

char h_pkt::getcmd()
{
    return CMD;
}

char* h_pkt::getdata()
{
    return data;
}

//h_eepread definitions

h_eepread::h_eepread() : h_pkt(9, 0xfe, 2)
{
    calcchk();
}

h_eepread::h_eepread(int _pID, int addr, int length) : h_pkt(9, _pID, 1)
{
    data[0] = addr;
    data[1] = length;
    calcchk();
}

//setter

void h_eepread::setsize(int _size)
{
}

void h_eepread::setcmd(int _cmd)
{
}

//h_eepwrite definitions

h_eepwrite::h_eepwrite() : h_pkt(9, 0xfe, 1)
{
    calcchk();
}

h_eepwrite::h_eepwrite(int _pID, int addr, int length, char* _data) : h_pkt(9, 0xfe, 1)
{
    data[0] = addr;
    data[1] = length;
    size = 9 + length;
    setdata(_data, length);
    setaddress(addr);
    calcchk();
}

//setter

void h_eepwrite::setsize(int _size)
{
}

void h_eepwrite::setcmd(int _cmd)
{
}

void h_eepwrite::setaddress(int addr)
{
    data[0] = addr;
    calcchk();
}

void h_eepwrite::setlength(int length)
{
    data[1] = length;
    calcchk();
}

void h_eepwrite::setdata(char* _data, int sz)
{
    setlength(sz);
    for (int i = 0; i < sz; i++) data[2+i] = _data[i];
    calcchk();
}

//h_ramread definitions

h_ramread::h_ramread() : h_pkt(9, 0xfe, 4)
{
    calcchk();
}

h_ramread::h_ramread(int _pID, int addr, int length) : h_pkt(9, _pID, 4)
{
    data[0] = addr;
    data[1] = length;
    calcchk();
}

//setter

void h_ramread::setsize(int _size)
{
}

void h_ramread::setcmd(int _cmd)
{
}

//h_ramwrite definitions

h_ramwrite::h_ramwrite() : h_pkt(9, 0xfe, 3)
{
    calcchk();
}

h_ramwrite::h_ramwrite(int _pID, int addr, int length, char* _data) : h_pkt(9, _pID, 3)
{
    data[0] = addr;
    data[1] = length;
    size = 9 + length;
    setdata(_data, length);
    setaddress(addr);
    calcchk();
}

//setter

void h_ramwrite::setsize(int _size)
{
}

void h_ramwrite::setcmd(int _cmd)
{
}

void h_ramwrite::setaddress(int addr)
{
    data[0] = addr;
    calcchk();
}

void h_ramwrite::setlength(int length)
{
    data[1] = length;
    calcchk();
}

void h_ramwrite::setdata(char* _data, int sz)
{
    setlength(sz);
    for (int i = 0; i < sz; i++) data[2+i] = _data[i];
    calcchk();
}

//h_ijog definitions

h_ijog::h_ijog() : h_pkt(7, 0xfe, 5), mcnt(0)
{
    calcchk();
}

h_ijog::h_ijog(int _pID) : h_pkt(7, _pID, 5), mcnt(0)
{
    calcchk();
}

//motor op

void h_ijog::addmot(int _pid, int pot, int SET, int time)
{
    char* dm = &data[mcnt*5 + 7];
    dm[0] = pot&0xFF;
    dm[1] = (pot >> 8)&0xFF;
    dm[2] = SET;
    dm[3] = _pid;
    dm[4] = time;
    mcnt++;
    calcchk();
}

bool h_ijog::hasmot(int _pid)
{
    for (int i = 0; i < mcnt; i++)
    {
        char* dm = &data[i*5 + 7];
        if(_pid == dm[3]) return true;
    }
    return false;
}

void h_ijog::remmot(int _pid)
{
    for (int i = 0; i < mcnt; i++)
    {
        char* dm = &data[i*5 + 7];
        if(_pid == dm[3])
        {
            char* ow = &data[(mcnt - 1)*5 + 7];
            dm[0] = ow[0];
            dm[1] = ow[1];
            dm[2] = ow[2];
            dm[3] = ow[3];
            dm[4] = ow[4];
            calcchk();
        }
    }
}

//setter

void h_ijog::setsize(int _size)
{
}

void h_ijog::setcmd(int _cmd)
{
}

void h_ijog::setdata(char* _data, int sz)
{
}

//h_sjog definitions

h_sjog::h_sjog() : h_pkt(7, 0xfe, 6), mcnt(0)
{
    calcchk();
}

h_sjog::h_sjog(int _pID) : h_pkt(7, _pID, 6), mcnt(0)
{
    calcchk();
}

//motor op

void h_sjog::addmot(int _pid, int pot, int SET)
{
    char* dm = &data[mcnt*4 + 8];
    dm[0] = pot&0xFF;
    dm[1] = (pot >> 8)&0xFF;
    dm[2] = SET;
    dm[3] = _pid;
    mcnt++;
    calcchk();
}

bool h_sjog::hasmot(int _pid)
{
    for (int i = 0; i < mcnt; i++)
    {
        char* dm = &data[i*4 + 7];
        if(_pid == dm[3]) return true;
    }
    return false;
}

void h_sjog::remmot(int _pid)
{
    for (int i = 0; i < mcnt; i++)
    {
        char* dm = &data[i*4 + 7];
        if(_pid == dm[3])
        {
            char* ow = &data[(mcnt - 1)*4 + 7];
            dm[0] = ow[0];
            dm[1] = ow[1];
            dm[2] = ow[2];
            dm[3] = ow[3];
            calcchk();
        }
    }
}


//setter

void h_sjog::setsize(int _size)
{
}

void h_sjog::setcmd(int _cmd)
{
}

void h_sjog::setdata(char* _data, int sz)
{
}

void h_sjog::settime(int time)
{
    data[0] = time;
    calcchk();
}

//h_stat definitions

h_stat::h_stat() : h_pkt(9, 0xfe, 8)
{
    calcchk();
}

h_stat::h_stat(int _pID) : h_pkt(7, _pID, 7)
{
    calcchk();
}

//setter

void h_stat::setsize(int _size)
{
}

void h_stat::setcmd(int _cmd)
{
}

void h_stat::setdata(char* _data, int sz)
{
}

//h_rollback definitions

h_rollback::h_rollback() : h_pkt(9, 0xfe, 8)
{
    data[0] = 0;
    data[1] = 0;
    calcchk();
}

h_rollback::h_rollback(int _pID, bool idskip = 0, bool bandskip = 0) : h_pkt(9, _pID, 8)
{
    data[0] = idskip;
    data[1] = bandskip;
    calcchk();
}

//setter

void h_rollback::setsize(int _size)
{
}

void h_rollback::setcmd(int _cmd)
{
}

void h_rollback::setdata(char* _data, int sz)
{
}

void h_rollback::setidskip(int idskip)
{
    data[0] = idskip;
    calcchk();
}

void h_rollback::setbandskip(int bandskip)
{
    data[1] = bandskip;
    calcchk();
}

//h_reboot definitions

h_reboot::h_reboot() : h_pkt(7, 0xfe, 9)
{
    calcchk();
}

h_reboot::h_reboot(int _pID) : h_pkt(7, _pID, 9)
{
    calcchk();
}

//setter

void h_reboot::setsize(int _size)
{
}

void h_reboot::setcmd(int _cmd)
{
}

void h_reboot::setdata(char* _data, int sz)
{
}

//h_motor definitions

h_motor::h_motor()
{
    pID = inv = calib = 0;
}

h_motor::h_motor(int _pID, bool inverted, float _calib) : pID(_pID), inv(inverted), calib(_calib)
{
}

//herkulex_chain definitions

herkulex_chain::herkulex_chain(char* s_port = "/dev/ttyAMA0", int baud = 115200)
{
    serial_fd = serialOpen(s_port, baud);
}

void herkulex_chain::writeeep(int addr, int size, char* data, int id)
{
    h_eepwrite packet(id, addr, size, data);
    sendp(packet);
}

void herkulex_chain::readeep(int addr, int size, char* data, int id, int tout)
{
    h_eepread packet(id, addr, size);
    sendp(packet);
    h_pkt ret;
    readp(ret, 100);
    for (int i = 0; i < ret.getdata()[1]; i++) data[i] = ret.getdata()[2+i]; 
}

void herkulex_chain::writeram(int addr, int size, char* data, int id)
{
    h_ramwrite packet(id, addr, size, data);
    sendp(packet);
}

void herkulex_chain::readram(int addr, int size, char* data, int id, int tout)
{
    h_ramread packet(id, addr, size);
    sendp(packet);
    h_pkt ret;
    readp(ret, tout);
    for (int i = 0; i < ret.getdata()[1]; i++) data[i] = ret.getdata()[2+i]; 
}

void herkulex_chain::setcolor(h_color color, int id = 0xfe)
{
    char c = color;
    
    writeram(RAMLED_CONTROL, 1, &c, id);
}

void herkulex_chain::clearerr(h_color color = green, int id = 0xfe)
{   
    char data[] = {0, 0};
    writeram(RAMSTAT_ERR, 2, data, id);
    
    setcolor(color);
}

void herkulex_chain::setspeed(int speed, h_color color = none, int id = 0xfe)
{

}

void herkulex_chain::setpos(int pos, h_color color = none, int id = 0xfe)
{

}

void herkulex_chain::addmot(int _pid, bool inv, float calib)
{
    if(!hasmot(_pid))
    {
        h_motor mot(_pid, inv, calib);
        motors.push_back(mot);
    }
}

bool herkulex_chain::hasmot(int _pid)
{
    for (int i = 0; i < motors.size(); i++)
    {
        if (motors[i].pID == _pid)return true;
    }
    return false;
}

void herkulex_chain::remmot(int _pid)
{
    for (int i = 0; i < motors.size(); i++)
    {
        if (motors[i].pID == _pid) motors.erase(motors.begin() + (i--));
    }
}

void herkulex_chain::sendp(h_pkt &packet)
{
    printf("Sending packet\n");
    for(int i = 0; i < packet.getsize(); i++) printf(((char*)&packet)[i] < 0x10?"0x0%x ":"0x%x ", ((char*)&packet)[i]);
    printf("\n");
    write(serial_fd, &packet, packet.getsize());
}

void herkulex_chain::readp(h_pkt &packet, unsigned int timeout=100)
{
    unsigned int t0 = millis();
    while(millis() - t0 < timeout || serialDataAvail(serial_fd) < 7){}
    if(millis() - t0 >= timeout) return;
    serialGetchar(serial_fd);
    serialGetchar(serial_fd);
    packet.setsize(serialGetchar(serial_fd));
    packet.setpid(serialGetchar(serial_fd));
    packet.setcmd(serialGetchar(serial_fd));
    serialGetchar(serial_fd);
    serialGetchar(serial_fd);
    
    char data[256];
    for (int i = 7; i < packet.getsize(); i++) data[7 + i] = serialGetchar(serial_fd);
    packet.setdata(data, packet.getsize() - 7);
}
