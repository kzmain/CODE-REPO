<?php

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

use App\Booking;

class BookingTest extends TestCase
{
    public function testValidInput()
    {
        $input = array(
            'user_id' => '1',
            'service_id' => '1',
            'employee_id' => '1',
            'date' => '2000-01-01',
            'day_of_week' => '1',
            'start_time' => '1200',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->passes());
    }
    public function testEmptyInput()
    {
        $input = array();
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidUser_id()
    {
        $input = array(
            'user_id' => 'a',
            'service_id' => '1',
            'employee_id' => '1',
            'date' => '2000-01-01',
            'day_of_week' => '1',
            'start_time' => '1200',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidService_id()
    {
        $input = array(
            'user_id' => '1',
            'service_id' => 'a',
            'employee_id' => '1',
            'date' => '2000-01-01',
            'day_of_week' => '1',
            'start_time' => '1200',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidEmployee_id()
    {
        $input = array(
            'user_id' => '1',
            'service_id' => '1',
            'employee_id' => 'a',
            'date' => '2000-01-01',
            'day_of_week' => '1',
            'start_time' => '1200',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidDate()
    {
        $input = array(
            'user_id' => '1',
            'service_id' => '1',
            'employee_id' => '1',
            'date' => 'abcd-01-01',
            'day_of_week' => '1',
            'start_time' => '1200',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidDayOfWeek()
    {
        $input = array(
            'user_id' => '1',
            'service_id' => '1',
            'employee_id' => '1',
            'date' => '2000-01-01',
            'day_of_week' => '8',
            'start_time' => '1200',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidStart_Time()
    {
        $input = array(
            'user_id' => '1',
            'service_id' => '1',
            'employee_id' => '1',
            'date' => '2000-01-01',
            'day_of_week' => '1',
            'start_time' => '2500',
        );
        $validator = Booking::validator($input);
        $this->assertTrue($validator->fails());
    }
}
