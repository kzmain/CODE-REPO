<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class B2_Register_CanRegisterTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanRegister()
    {
        $this->visit('/register')
            ->type('Steve Jobs', 'name')
            ->type('1 Infinite Loop', 'address')
            ->type('Cupertino', 'city')
            ->select('NSW', 'state')
            ->type('2000', 'postcode')
            ->type('0412345678', 'phone')
            ->type('steve@apple.com', 'email')
            ->type('aA1aA1', 'password')
            ->type('aA1aA1', 'password_confirmation')
            ->press('Register')
            ->seePageIs('/home');
    }
}
