<?php

/*

The Booking class represents a booking for a user (customer) with an employee, for a
service, on a specified date and start_time. The duration is provided by the service.
The day_of_week is for convenience.

*/

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Validator;

class Booking extends Model
{
    protected $fillable = ['user_id', 'service_id', 'employee_id', 'date', 'day_of_week', 'start_time'];

    /* This is a validator for sanity checking and unit testing */
    public static function validator(array $data) {
        return Validator::make($data, [
            'user_id' => 'required|integer|min:0',
            'service_id' => 'required|integer|min:0',
            'employee_id' => 'required|integer|min:0',
            'date' => 'required|regex:/^\d{4}\-\d{2}\-\d{2}$/',
            'day_of_week' => 'required|integer|min:1|max:7',
            'start_time' => 'required|valid24hourtime',
        ],
        [
            'valid24hourtime' => 'Not a valid time'
        ]);
    }

    /* Each booking belongs to a user */
    public function user() {
        return $this->belongsTo(User::class);
    }

    /* Each booking belongs to an employee */
    public function employee() {
        return $this->belongsTo(Employee::class);
    }

    /* Each booking belongs to a service */
    public function service() {
        return $this->belongsTo(Service::class);
    }

    /* Extract the year from the date */
    public function year() {
        return explode('-', $this->date)[0];
    }

    /* Extract the month from the date */
    public function month() {
        return explode('-', $this->date)[1];
    }

    /* Extract the day from the date */
    public function day() {
        return explode('-', $this->date)[2];
    }

    /* Return the day_of_week as text instead of a number */
	public function day_of_week_as_text() {
        if ($this->day_of_week == 1) {
            return 'Sunday';
        }
        if ($this->day_of_week == 2) {
            return 'Monday';
        }
        if ($this->day_of_week == 3) {
            return 'Tuesday';
        }
        if ($this->day_of_week == 4) {
            return 'Wednesday';
        }
        if ($this->day_of_week == 5) {
            return 'Thursday';
        }
        if ($this->day_of_week == 6) {
            return 'Friday';
        }
        if ($this->day_of_week == 7) {
            return 'Saturday';
        }

        return 'Invalid Day of Week';
    }
}
