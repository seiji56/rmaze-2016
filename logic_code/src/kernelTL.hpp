#ifndef _KERNELTL_HPP_
#define _KERNELTL_HPP_

#include <stdio.h>
#include <Python.h>

#include "logic_util.hpp"
#include "defines.hpp"

namespace kernelTL
{
    void init();
    void clean();

    PyObject *pylibs;

	namespace out
	{
		namespace others
		{
			void zeroTimer ();
		}

		namespace locomotion
		{
            PyObject *execute_fn;
			int execute (logic::action action);
		}
	}

	namespace in
	{
		namespace sensors
		{
            PyObject *color_fn;
            PyObject *distance_fn;
            int color ();
			int distance (byte d);
		}
	}
}

#endif
