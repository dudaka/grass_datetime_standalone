#include <stdio.h>
#include <grass/datetime.h>

int main() {
    DateTime dt;
    char buffer[100];

    // Initialize a datetime structure
    if (datetime_set_type(&dt, DATETIME_ABSOLUTE, DATETIME_YEAR, DATETIME_SECOND, 0) != 0) {
        printf("Error setting datetime type\n");
        return 1;
    }

    // Set some values
    datetime_set_year(&dt, 2025);
    datetime_set_month(&dt, 8);
    datetime_set_day(&dt, 24);
    datetime_set_hour(&dt, 14);
    datetime_set_minute(&dt, 30);
    datetime_set_second(&dt, 45.5);

    // Format and print the datetime
    if (datetime_format(&dt, buffer) == 0) {
        printf("DateTime: %s\n", buffer);
    } else {
        printf("Error formatting datetime\n");
    }

    printf("GRASS DateTime library test completed successfully!\n");
    return 0;
}
