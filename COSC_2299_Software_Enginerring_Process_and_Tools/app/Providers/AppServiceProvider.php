<?php

namespace App\Providers;

use Laravel\Dusk\DuskServiceProvider;
use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Schema;
use App\Employee;
use App\Booking;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
		Schema::defaultStringLength(191);/*This is for windows*/
		
        /* This is a custom validator, it checks for a valid 24 hour time */
        Validator::extend('valid24hourtime', function ($attribute, $value, $parameters, $validator) {
            if (!preg_match('/^[0-9]*$/', $value)) {
                return false;
            }
            if ($value == '') {
                return true;
            }
            $num = intval($value);
            
//            $hour = intdiv($num, 100);
            $hour = (int)floor($num / 100.0);
            $min = $num % 100;

            if ($min >= 60) {
                return false;
            }
            if ($hour >= 24) {
                return false;
            }
            return true;
        });

        /* This is a custom validator, it compares two integer fields */
        Validator::extend('greaterthanintegerfield', function($attribute, $value, $parameters, $validator) {
            $data = $validator->getData();
            $minValue = $data[$parameters[0]];
            return $value > $minValue;
        });   

        /* This is a custom validator, it checks for alphabetic characters and spaces */
        Validator::extend('lettersandspacesonly', function($attribute, $value) {
            return preg_match('/^[\pL\s]+$/u', $value);
        });

    }

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        /* This is for Dusk testing */
        if ($this->app->environment('local', 'testing')) {
            $this->app->register(DuskServiceProvider::class);
        }
    }

    /* Return the month as text */
    public static function month_as_text($val) {
        $val = intval($val);
        if ($val == 1) { return 'January'; }
        if ($val == 2) { return 'February'; }
        if ($val == 3) { return 'March'; }
        if ($val == 4) { return 'April'; }
        if ($val == 5) { return 'May'; }
        if ($val == 6) { return 'June'; }
        if ($val == 7) { return 'July'; }
        if ($val == 8) { return 'August'; }
        if ($val == 9) { return 'September'; }
        if ($val == 10) { return 'October'; }
        if ($val == 11) { return 'November'; }
        if ($val == 12) { return 'December'; }
        return 'Invalid Month';
    }

    /* Return the month as text (shortened) */
    public static function month_as_short_text($val) {
        $val = intval($val);
        if ($val == 1) { return 'Jan'; }
        if ($val == 2) { return 'Feb'; }
        if ($val == 3) { return 'Mar'; }
        if ($val == 4) { return 'Apr'; }
        if ($val == 5) { return 'May'; }
        if ($val == 6) { return 'Jun'; }
        if ($val == 7) { return 'Jul'; }
        if ($val == 8) { return 'Aug'; }
        if ($val == 9) { return 'Sep'; }
        if ($val == 10) { return 'Oct'; }
        if ($val == 11) { return 'Nov'; }
        if ($val == 12) { return 'Dec'; }
        return 'Invalid Month';
    }

    /* Return the day of week as text */
    public static function day_of_week_as_text($val) {
        if ($val == 1) { return 'Sunday'; }
        if ($val == 2) { return 'Monday'; }
        if ($val == 3) { return 'Tuesday'; }
        if ($val == 4) { return 'Wednesday'; }
        if ($val == 5) { return 'Thursday'; }
        if ($val == 6) { return 'Friday'; }
        if ($val == 7) { return 'Saturday'; }
        return 'Invalid Day of Week';
    }

    /*
        This takes a 24-hour time $a and adds $b minutes to it and returns the results
        For example: add_minutes(1230, 60) would return 1330
    */
    public static function add_minutes($a, $b) {
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
        Returns an associative array for the day that is $i days from today
        For example: If $i is 1 then that is tomorrow
    */
    public static function getDateFromToday($i) {
        $timestamp = strtotime('+' . $i . ' day');
        $elt = array();
        $elt['year'] = date('Y', $timestamp);
        $elt['month'] = date('m', $timestamp);
        $elt['month_as_text'] = date('M', $timestamp);
        $elt['day'] = date('d', $timestamp);
        $elt['day_of_week'] = date('w', $timestamp) + 1;
        $elt['date'] = date('Y-m-d', $timestamp);
        return $elt;
    }

    /*
        Returns an associative array for today, like the above function getDateFromToday()
    */
    public static function getCurrentDate() {
        return \App\Providers\AppServiceProvider::getDateFromToday(0);
    }

    /*
        Returns an array of associative arrays provided by getDateFromToday()
    */
    public static function getNextDays($start, $end) {
        $dates = array();
        for ($i=$start; $i<=$end; $i++) {
            $dates[] = \App\Providers\AppServiceProvider::getDateFromToday($i);
        }
        return $dates;
    }
}
