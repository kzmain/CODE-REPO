<?php

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

use App\Employee;

class EmployeeTest extends TestCase
{
    public function testValidInput()
    {
        $input = array(
            'name' => 'Joe Blow',
            'email' => 'joe@example.com',
            'address' => '1 Main St',
            'city' => 'Anytown',
            'state' => 'NSW',
            'postcode' => '2000',
            'phone' => '0412345678'
        );
        $validator = Employee::validator($input);
        $this->assertTrue($validator->passes());
    }
    public function testEmptyInput()
    {
        $input = array(
        );
        $validator = Employee::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidEmail()
    {
        $input = array(
            'name' => 'Joe Blow',
            'email' => 'joe example com',
            'address' => '1 Main St',
            'city' => 'Anytown',
            'state' => 'NSW',
            'postcode' => '2000',
            'phone' => '0412345678'
        );
        $validator = Employee::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidState()
    {
        $input = array(
            'name' => 'Joe Blow',
            'email' => 'joe@example.com',
            'address' => '1 Main St',
            'city' => 'Anytown',
            'state' => 'CA',
            'postcode' => '2000',
            'phone' => '0412345678'
        );
        $validator = Employee::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidPostcode()
    {
        $input = array(
            'name' => 'Joe Blow',
            'email' => 'joe@example.com',
            'address' => '1 Main St',
            'city' => 'Anytown',
            'state' => 'NSW',
            'postcode' => 'abc',
            'phone' => '0412345678'
        );
        $validator = Employee::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidPhone()
    {
        $input = array(
            'name' => 'Joe Blow',
            'email' => 'joe@example.com',
            'address' => '1 Main St',
            'city' => 'Anytown',
            'state' => 'NSW',
            'postcode' => '2000',
            'phone' => '212-555-1212'
        );
        $validator = Employee::validator($input);
        $this->assertTrue($validator->fails());
    }
}
