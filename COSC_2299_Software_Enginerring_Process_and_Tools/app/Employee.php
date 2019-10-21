<?php

/*

The Employee class represents an employee. It's a strange world, indeed.

*/

namespace App;

use App\Availability;
use App\Booking;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Validator;

class Employee extends Model
{
    //
    protected $fillable = ['name', 'address', 'city', 'state', 'postcode', 'email', 'phone', 'email'];

    /* This is a validator for sanity checking and unit testing */
    public static function validator(array $data) {
        return Validator::make($data, [
            'name' => 'required|max:255|lettersandspacesonly',
            'email' => 'required|email|max:255|unique:employees',
            'address' => 'required|max:255',
            'city' => 'required|max:255|lettersandspacesonly',
            'state' => 'required|in:NSW,VIC,QLD,TAS,SA,NT,WA',
            'postcode' => 'required|digits:4',
            'phone' => 'required|digits:10|regex:/^0[23478][0-9]{8}$/'
        ],
        [
            'lettersandspacesonly' => 'Can only contain letters and spaces.'
        ]);
    }

    /* Each employee belongs to a business */
    public function business() {
        return $this->belongsTo('App\Business');
    }

    /* An employee has many availabilities, as many as one for each day of the week */
    public function availabilities() {
        return $this->hasMany(Availability::class)->orderBy('day_of_week');
    }

    /* This returns the availability for a particular day of the week (numeric, 1=Sunday) */
    public function availability($i) {
        $results = $this->availabilities()->where('day_of_week', '=', $i);
        if ($results) {
            $elt = $results->first();
            if ($elt) {
                if ($elt->end_time) {
                    return $elt;
                }
            }
        }
        return null;
    }

    /*
        This takes a 24-hour time $a and adds $b minutes to it and returns the results
        For example: add_minutes(1230, 60) would return 1330
    */
    public function add_minutes($a, $b) {
        $hourA = intval($a / 100);
        $minA = $a % 100;
        $hourB = intval($b / 60);
        $minB = $b % 60;
        $hourSum = $hourA + $hourB;
        $minSum = $minA + $minB;
        $hourNorm = $hourSum + intval($minSum / 60);
        $minNorm = $minSum % 60;
        return $hourNorm * 100 + $minNorm;
    }

    /*
        This returns all the available bookings with an employee, for a user and service,
        on a specified day of the week
        The result is a collection of associative arrays, not a collection of objects
    */
    public function availableBookings($user, $service, $day_of_week) {
        $currentDate = \App\Providers\AppServiceProvider::getCurrentDate();

        $results = array();
        $availability = $this->availability($day_of_week);
        if ($availability) {
            $start_time = $availability->start_time;
            for(;;) {
                $start_time = $this->nextAvailableTime($currentDate, $user, $day_of_week, $start_time, $service->duration_in_minutes);
                if ($this->add_minutes($start_time, $service->duration_in_minutes) > $availability->end_time) {
                    break;
                }
                $results[] = array(
                    'user' => $user,
                    'service' => $service,
                    'employee' => $this,
                    'day_of_week' => $day_of_week,
                    'start_time' => $start_time
                );
                $start_time = $this->add_minutes($start_time, $service->duration_in_minutes);
            }
        }
        return collect($results);
    }

    /*
        This is used by availableBookings() to calculate the next available time given
        the constraints
    */
    public function nextAvailableTime($currentDate, $user, $day_of_week, $start_time, $duration_in_minutes) {
        $userBookings = Booking::all()
            ->where('user_id', '=', $user->id)
            ->where('day_of_week', '=', $day_of_week)
            ->where('date', '>=', $currentDate['date']);
        $end_time = $this->add_minutes($start_time, $duration_in_minutes);
        $bookings = Booking::all()
                ->where('employee_id', '=', $this->id)
                ->where('day_of_week', '=', $day_of_week)
                ->where('date', '>=', $currentDate['date']);
        $bookings = $bookings->merge($userBookings);
        $latest_time = $start_time;
        $flag = 0;
        foreach ($bookings as $booking) {
            $booking_start_time = $booking->start_time;
            $booking_end_time = $this->add_minutes($booking_start_time, $booking->service->duration_in_minutes);
            if ($end_time <= $booking_start_time) {
                continue;
            }
            if ($start_time >= $booking_end_time) {
                continue;
            }
            if (!$flag || ($booking_end_time > $latest_time)) {
                $latest_time = $booking_end_time;
                $flag = 1;
            }
        }
        if ($flag) {
            return $this->nextAvailableTime($currentDate, $user, $day_of_week, $latest_time, $duration_in_minutes);
        }
        return $start_time;
    }

    /* Check to see if a booking is available, for validation */
    public function isBookingAvailable($user, $service, $day_of_week, $start_time) {
        $bookings = $this->availableBookings($user, $service, $day_of_week);
        if (!$bookings) {
            return false;
        }
        foreach ($bookings as $booking) {
            if ($booking['start_time'] == $start_time) {
                return true;
            }
        }
        return false;
    }

}
