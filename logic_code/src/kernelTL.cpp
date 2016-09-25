#include "kernelTL.hpp"

void kernelTL::init()
{
    printf("Initiating python...\n");
    Py_Initialize();
    PyObject* pylibs_name = PyBytes_FromString((char*)"pylib.base_lib");
    pylibs = PyImport_Import(pylibs_name);

    printf("Loading python functions...\n");
    out::locomotion::execute_fn = PyObject_GetAttrString(pylibs, (char*)"out_loc_execute");
    printf("Loaded out functions.\n");
    in::sensors::color_fn = PyObject_GetAttrString(pylibs, (char*)"in_sensors_color");
    in::sensors::distance_fn = PyObject_GetAttrString(pylibs, (char*)"in_sensors_distance");
    printf("Loaded in functions.\n");
    printf("Initialized!\n");
}

void kernelTL::clean()
{
    Py_Finalize();
}

void kernelTL::out::others::zeroTimer ()
{
}

int kernelTL::out::locomotion::execute (logic::action action)
{
    PyObject* args = PyTuple_Pack(action.type, action.cnt);
    PyObject* result = PyObject_CallObject(execute_fn, args);
	return (int) PyList_Size(result);
}

int kernelTL::in::sensors::color ()
{
    PyObject* result = PyObject_CallObject(color_fn, 0);
	return (int) PyList_Size(result);
}

int kernelTL::in::sensors::distance (byte d)
{
    PyObject* args = Py_BuildValue("i", d);
    PyObject* result = PyObject_CallObject(distance_fn, args);
	return (int) PyList_Size(result);
}
