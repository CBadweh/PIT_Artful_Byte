#include "trace.h"
#include "printf_config.h"
#include "printf.h"

void trace(const char *format, ...)
{
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}
