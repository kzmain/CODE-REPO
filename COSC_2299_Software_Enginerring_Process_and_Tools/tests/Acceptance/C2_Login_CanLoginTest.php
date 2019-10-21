<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class C2_Login_CanLoginTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanLogin()
    {
        $this->visit('/login')
            ->type('steve@apple.com', 'email')
            ->type('aA1aA1', 'password')
            ->press('Login')
            ->seePageIs('/home');
    }
}
