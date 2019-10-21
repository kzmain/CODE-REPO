<?php

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

use App\User;

class RegisterTest extends TestCase
{
    public function testValidInput()
    {
        $input = array(
            'name' => 'Pocahontas',
            'email' => 'pocahontas@disney.com',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8Disney',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'NT',
            'postcode' => '1234',
            'phone' => '0412345678'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->passes());
    }
    public function testEmptyInput()
    {
        $input = array();
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidEmail()
    {
        $input = array(
            'name' => 'Pocahontas',
            'email' => 'pocahontas disney com',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8Disney',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'NT',
            'postcode' => '1234',
            'phone' => '0412345678'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testMissingEmail()
    {
        $input = array(
            'name' => 'Pocahontas',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8Disney',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'NT',
            'postcode' => '1234',
            'phone' => '0412345678'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testPasswordMismatch()
    {
        $input = array(
            'name' => 'Pocahontas',
            'email' => 'pocahontas@disney.com',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8DisneyAlot',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'NT',
            'postcode' => '1234',
            'phone' => '0412345678'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidState()
    {
        $input = array(
            'name' => 'Pocahontas',
            'email' => 'pocahontas@disney.com',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8Disney',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'CA',
            'postcode' => '1234',
            'phone' => '0412345678'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidPostcode()
    {
        $input = array(
            'name' => 'Pocahontas',
            'email' => 'pocahontas@disney.com',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8Disney',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'NT',
            'postcode' => 'abc',
            'phone' => '0412345678'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
    public function testInvalidPhone()
    {
        $input = array(
            'name' => 'Pocahontas',
            'email' => 'pocahontas@disney.com',
            'password' => 'iH8Disney',
            'password_confirmation' => 'iH8Disney',
            'address' => '1 Main St',
            'city' => 'Disneyland',
            'state' => 'NT',
            'postcode' => '1234',
            'phone' => '212-555-1212'
        );
        $validator = User::validator($input);
        $this->assertTrue($validator->fails());
    }
}
