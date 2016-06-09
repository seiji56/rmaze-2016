#include "types.hpp"


//Distance def.

types::dist::dist(double cm) : raw(cm)
{
}

double types::dist::cm()
{
    return raw;
}

double types::dist::mm()
{
    return raw*10;
}

double types::dist::m()
{
    return raw/100;
}

double types::dist::tiles()
{
    return raw/30;
}

types::dist types::dist::operator+(types::dist d)
{
    return types::dist(cm() + d.cm());
}

types::dist types::dist::operator-(types::dist d)
{
    return types::dist(cm() - d.cm());
}

types::dist types::dist::operator*(double m)
{
    return types::dist(cm()*m);
}

types::dist types::dist::operator/(double d)
{
    return types::dist(cm()/d);
}

types::dist types::dist::operator+=(types::dist d)
{
    raw += d.cm();
    return *this;
}

types::dist types::dist::operator-=(types::dist d)
{
    raw -= d.cm();
    return *this;
}

//Temperature def.
types::temp::temp(double deg) : raw(deg)
{
}

double types::temp::deg()
{
    return raw;
}

double types::temp::far()
{
    return raw*(9/5) + 32;
}

double types::temp::kel()
{
    return raw + 273.15;
}

types::temp types::temp::operator+(types::temp d)
{
    return types::temp(deg() + d.deg());
}

types::temp types::temp::operator*(double m)
{
    return types::temp(deg()*m);
}

types::temp types::temp::operator/(double d)
{
    return types::temp(deg()*d);
}

types::temp types::temp::operator-(types::temp d)
{
    return types::temp(deg() - d.deg());
}

types::temp types::temp::operator+=(types::temp d)
{
    raw += d.deg();
    return *this;
}

types::temp types::temp::operator-=(types::temp d)
{
    raw -= d.deg();
    return *this;
}


//Time def.
types::time::time(double millis) : raw(millis)
{
}

double types::time::mil()
{
    return raw;
}

double types::time::sec()
{
    return raw/1000;
}

double types::time::min()
{
    return sec()/60;
}

types::time types::time::operator+(types::time d)
{
    return types::time(mil() + d.mil());
}

types::time types::time::operator*(double m)
{
    return types::time(mil()*m);
}

types::time types::time::operator/(double d)
{
    return types::time(mil()*d);
}

types::time types::time::operator-(types::time d)
{
    return types::time(mil() - d.mil());
}

types::time types::time::operator+=(types::time d)
{
    raw += d.mil();
    return *this;
}

types::time types::time::operator-=(types::time d)
{
    raw -= d.mil();
    return *this;
}
