#ifndef GRASS_DATETIMEDEFS_H
#define GRASS_DATETIMEDEFS_H

#ifdef _WIN32
    #ifdef GRASS_DATETIME_DLL_EXPORT
        #define GRASS_DATETIME_API __declspec(dllexport)
    #else
        #define GRASS_DATETIME_API __declspec(dllimport)
    #endif
#else
    #define GRASS_DATETIME_API
#endif

/* between.c */
GRASS_DATETIME_API int datetime_is_between(int x, int a, int b);

/* change.c */
GRASS_DATETIME_API int datetime_change_from_to(DateTime *dt, int from, int to, int round);

/* copy.c */
GRASS_DATETIME_API void datetime_copy(DateTime *src, const DateTime *dst);

/* diff.c */
GRASS_DATETIME_API int datetime_difference(const DateTime *a, const DateTime *b, DateTime *result);

/* error.c */
GRASS_DATETIME_API int datetime_error(int code, char *msg);
GRASS_DATETIME_API int datetime_error_code(void);
GRASS_DATETIME_API char *datetime_error_msg(void);
GRASS_DATETIME_API void datetime_clear_error(void);

/* format.c */
GRASS_DATETIME_API int datetime_format(const DateTime *dt, char *buf);

/* incr1.c */
GRASS_DATETIME_API int datetime_increment(DateTime *src, DateTime *incr);

/* incr2.c */
GRASS_DATETIME_API int datetime_is_valid_increment(const DateTime *src, const DateTime *incr);
GRASS_DATETIME_API int datetime_check_increment(const DateTime *src, const DateTime *incr);

/* incr3.c */
GRASS_DATETIME_API int datetime_get_increment_type(const DateTime *dt, int *mode, int *from,
                                int *to, int *fracsec);
GRASS_DATETIME_API int datetime_set_increment_type(const DateTime *src, DateTime *incr);

/* local.c */
GRASS_DATETIME_API int datetime_get_local_timezone(int *minutes);
GRASS_DATETIME_API void datetime_get_local_time(DateTime *dt);

/* misc.c */
GRASS_DATETIME_API int datetime_days_in_month(int year, int month, int ad);
GRASS_DATETIME_API int datetime_is_leap_year(int year, int ad);
GRASS_DATETIME_API int datetime_days_in_year(int year, int ad);

/* same.c */
GRASS_DATETIME_API int datetime_is_same(const DateTime *src, const DateTime *dst);

/* scan.c */
GRASS_DATETIME_API int datetime_scan(DateTime *dt, const char *buf);

/* sign.c */
GRASS_DATETIME_API int datetime_is_positive(const DateTime *dt);
GRASS_DATETIME_API int datetime_is_negative(const DateTime *dt);
GRASS_DATETIME_API void datetime_set_positive(DateTime *dt);
GRASS_DATETIME_API void datetime_set_negative(DateTime *dt);
GRASS_DATETIME_API void datetime_invert_sign(DateTime *dt);

/* type.c */
GRASS_DATETIME_API int datetime_set_type(DateTime *dt, int mode, int from, int to, int fracsec);
GRASS_DATETIME_API int datetime_get_type(const DateTime *dt, int *mode, int *from, int *to,
                      int *fracsec);
GRASS_DATETIME_API int datetime_is_valid_type(const DateTime *dt);
GRASS_DATETIME_API int datetime_check_type(const DateTime *dt);
GRASS_DATETIME_API int datetime_in_interval_year_month(int x);
GRASS_DATETIME_API int datetime_in_interval_day_second(int x);
GRASS_DATETIME_API int datetime_is_absolute(const DateTime *dt);
GRASS_DATETIME_API int datetime_is_relative(const DateTime *dt);

/* tz1.c */
GRASS_DATETIME_API int datetime_check_timezone(const DateTime *dt, int minutes);
GRASS_DATETIME_API int datetime_get_timezone(const DateTime *dt, int *minutes);
GRASS_DATETIME_API int datetime_set_timezone(DateTime *dt, int minutes);
GRASS_DATETIME_API int datetime_unset_timezone(DateTime *dt);
GRASS_DATETIME_API int datetime_is_valid_timezone(int minutes);

/* tz2.c */
GRASS_DATETIME_API int datetime_change_timezone(DateTime *dt, int minutes);
GRASS_DATETIME_API int datetime_change_to_utc(DateTime *dt);
GRASS_DATETIME_API void datetime_decompose_timezone(int tz, int *hours, int *minutes);

/* values.c */
GRASS_DATETIME_API int datetime_check_year(const DateTime *dt, int year);
GRASS_DATETIME_API int datetime_check_month(const DateTime *dt, int month);
GRASS_DATETIME_API int datetime_check_day(const DateTime *dt, int day);
GRASS_DATETIME_API int datetime_check_hour(const DateTime *dt, int hour);
GRASS_DATETIME_API int datetime_check_minute(const DateTime *dt, int minute);
GRASS_DATETIME_API int datetime_check_second(const DateTime *dt, double second);
GRASS_DATETIME_API int datetime_check_fracsec(const DateTime *dt, int fracsec);
GRASS_DATETIME_API int datetime_get_year(const DateTime *dt, int *year);
GRASS_DATETIME_API int datetime_set_year(DateTime *dt, int year);
GRASS_DATETIME_API int datetime_get_month(const DateTime *dt, int *month);
GRASS_DATETIME_API int datetime_set_month(DateTime *dt, int month);
GRASS_DATETIME_API int datetime_get_day(const DateTime *dt, int *day);
GRASS_DATETIME_API int datetime_set_day(DateTime *dt, int day);
GRASS_DATETIME_API int datetime_get_hour(const DateTime *dt, int *hour);
GRASS_DATETIME_API int datetime_set_hour(DateTime *dt, int hour);
GRASS_DATETIME_API int datetime_get_minute(const DateTime *dt, int *minute);
GRASS_DATETIME_API int datetime_set_minute(DateTime *dt, int minute);
GRASS_DATETIME_API int datetime_get_second(const DateTime *dt, double *second);
GRASS_DATETIME_API int datetime_set_second(DateTime *dt, double second);
GRASS_DATETIME_API int datetime_get_fracsec(const DateTime *dt, int *fracsec);
GRASS_DATETIME_API int datetime_set_fracsec(DateTime *dt, int fracsec);

#endif /* GRASS_DATETIMEDEFS_H */
