<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class B6_Register_DetectInvalidEmailTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testDetectInvalidEmail()
    {
        $this->visit('/register')
            ->type('Steve Jobs', 'name')
            ->type('1 Infinite Loop', 'address')
            ->type('Cupertino', 'city')
            ->select('NSW', 'state')
            ->type('3000', 'postcode')
            ->type('0412345678', 'phone')
            ->type('steve@apple', 'email')
            ->type('aA1aA1', 'password')
            ->type('aA1aA1', 'password_confirmation')
            ->press('Register')
            ->see('The email must be a valid email address');
    }
}
