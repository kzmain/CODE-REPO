<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class B5_Register_DetectPasswordTooShortTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testDetectPasswordTooShort()
    {
        $this->visit('/register')
            ->type('Steve Jobs', 'name')
            ->type('1 Infinite Loop', 'address')
            ->type('Cupertino', 'city')
            ->select('NSW', 'state')
            ->type('3000', 'postcode')
            ->type('0412345678', 'phone')
            ->type('steve@apple.com', 'email')
            ->type('aA1', 'password')
            ->type('aA1', 'password_confirmation')
            ->press('Register')
            ->see('The password must be at least 6 characters');
    }
}
