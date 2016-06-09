#include <map>
#include <string>

#ifndef _TYPES
#define _TYPES

namespace types
{
    enum side
    {
        FRONT = 1,
        RIGHT = 2,
        BACK  = 3,
        LEFT  = 4,
        NONE = -1
    };

    enum color
    {
        WHITE,
        BLACK,
        SILVER
    };

    //distance
    struct dist
    {
    public:
        dist(double cm);

        double mm();
        double cm();
        double m();
        double tiles();

        types::dist operator+(types::dist d);
        types::dist operator-(types::dist d);
        types::dist operator*(double m);
        types::dist operator/(double d);
        types::dist operator+=(types::dist d);
        types::dist operator-=(types::dist d);
    private:
        double raw; //Raw data in centimeters
    };

    //Temperature
    struct temp
    {
    public:
        temp(double celsius);

        double deg();
        double far();
        double kel();


        types::temp operator+(types::temp d);
        types::temp operator-(types::temp d);
        types::temp operator*(double m);
        types::temp operator/(double d);
        types::temp operator+=(types::temp d);
        types::temp operator-=(types::temp d);
    private:
        double raw;//Raw data in degrees celsius
    };

    //Time
    struct time
    {
    public:
        time(double millis);

        double mil();
        double sec();
        double min();


        types::time operator+(types::time d);
        types::time operator-(types::time d);
        types::time operator*(double m);
        types::time operator/(double d);
        types::time operator+=(types::time d);
        types::time operator-=(types::time d);
    private:
        double raw;//Raw data in milliseconds
    };

    //IOIOevent

    namespace IOIO
    {
        namespace event
        {
            enum type
            {
                BUTTON_PRESSED,
                SLIDER_CHANGED,
                EM_STOP,
                APP_CLOSED,
                DISCONNECTED,
            };
        }
        struct IOIOevn
        {
        public:
            IOIOevn(std::string evn);
        private:
            std::string extra_data;
        };
    }

}

#endif // _TYPES
