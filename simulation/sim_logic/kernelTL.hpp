#include "types.hpp"
#include "kernelML.hpp"

#ifndef _KERNEL_TL
#define _KERNEL_TL

namespace kernel
{
    class kernel_tl
    {
    public:
        kernel_tl(kernel_ml *_mid_layer, unsigned int millis);

    protected:
        //OUTPUT
        //Locomotion
        bool out_walk (int tiles, int* expected = (int*)-1);
        void out_turn (int times);
        float out_align (int tout);
        void out_ramp ();
        //Others
        void out_drop (types::side where);
        void out_blink ();
        void out_IOIOupdate ();
        types::time sys_time();
        //void herkulexled();

        //INPUT

        //Sensors
        types::temp in_temp(types::side where);
        types::dist in_dist(types::side where);
        types::color in_color();
        types::side in_ramp();
        //Others
        bool IOIOavailable();
        bool IOIOpoll(types::IOIO::IOIOevn &evn);

        bool in_button(int gpio);
        void button_int(int gpio, void (*callback)());

    private:
        std::map<int, void (*)()> gpio_callback;
        kernel_ml *mid_layer;
        unsigned int start_mill;
    };

}

#endif // _KERNEL_TL
