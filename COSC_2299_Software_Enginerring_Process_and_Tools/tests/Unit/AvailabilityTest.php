<?php

/**
 *
 * Unit tests for the Availability class
 * 
 */

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

use App\Availability;

class AvailabilityTest extends TestCase
{
    /**
     *  Test for valid input
     *
     *
     */
    public function testValidInput()
    {
        $input = array(
            'employee_id' => 1,
            'day_of_week' => 1,
            'start_time' => 900,
            'end_time' => 1700
        );
        $validator = Availability::validator($input);
        $this->assertTrue($validator->passes());
    }

    /**
     *  Test for empty input
     *
     *
     */
    public function testEmptyInput()
    {
        $input = array(
        );
        $validator = Availability::validator($input);
        $this->assertTrue($validator->fails());
    }

    /**
     *  Test for invalid start time
     *
     *
     */
    public function testInvalidStartTime()
    {
        $input = array(
            'employee_id' => 1,
            'day_of_week' => 1,
            'start_time' => 'abc',
            'end_time' => 1700
        );
        $validator = Availability::validator($input);
        $this->assertTrue($validator->fails());
    }

    /**
     *  Test for invalid end time
     *
     *
     */
    public function testInvalidEndTime()
    {
        $input = array(
            'employee_id' => 1,
            'day_of_week' => 1,
            'start_time' => 900,
            'end_time' => 'abc'
        );
        $validator = Availability::validator($input);
        $this->assertTrue($validator->fails());
    }

    /**
     *  Test for end time before start time
     *
     *
     */
    public function testEndTimeBeforeStartTime()
    {
        $input = array(
            'employee_id' => 1,
            'day_of_week' => 1,
            'start_time' => 900,
            'end_time' => 800
        );
        $validator = Availability::validator($input);
        $this->assertTrue($validator->fails());
    }

    /**
     *  Test for invalid time with invalid seconds
     *
     *
     */
    public function testSecondsTooHigh()
    {
        $input = array(
            'employee_id' => 1,
            'day_of_week' => 1,
            'start_time' => 900,
            'end_time' => 1799
        );
        $validator = Availability::validator($input);
        $this->assertTrue($validator->fails());
    }
}
