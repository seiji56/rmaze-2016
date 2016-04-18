#include <wiringSerial.h>
#include <stdio.h>
#include <unistd.h>
#include <string>

struct pkt
{
    pkt() : header1(0xFF), header2(0xFF)
    {
    }

    char header1;
    char header2;
    char size;
    char pID;
    char CMD;
    char chk1;
    char chk2;
    char data[256];
    
    void calcchk()
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
};

void doit(int argc, char** argv, int serial_fd)
{
    printf("%d\n", serial_fd);
    pkt packet;
    
    packet.size = 0x07;
    packet.pID = 0xfe;
    packet.CMD = 0x07;
    
    
    
    packet.size = 0x0a;
    packet.pID = 0x03;
    packet.CMD = 0x03;
    
    /**/
    
    char data[] = {0x35, 0x01, 0x03, 0x03, 0x3c};
    
    for(int i = 0; i < packet.size - 7; i++) packet.data[i] = data[i];
    packet.calcchk();
    for(int i = 0; i < packet.size; i++) printf(((char*)&packet)[i] < 0x10?"0x0%x ":"0x%x ", ((char*)&packet)[i]);
    printf("\n");
    write(serial_fd, &packet, packet.size);
}

void readit(int serial_fd)
{
    while(1)
    {
        int rec = serialGetchar(serial_fd);
        if(rec >= 0)printf(rec < 0x10?"0x0%x ":"0x%x ", rec);
    }
}

int main(int argc, char** argv)
{
    
    int serial_fd = serialOpen(argc > 1? argv[1]:"/dev/ttyAMA0", 115200);
    doit(argc, argv, serial_fd);
    
    readit(serial_fd);
    serialClose(serial_fd);
}
