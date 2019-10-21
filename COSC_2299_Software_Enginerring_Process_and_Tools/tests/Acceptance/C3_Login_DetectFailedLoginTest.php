<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class C3_Login_DetectFailedLoginTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testDetectFailedLoginTest()
    {
        $this->visit('/login')
            ->type('steve@apple.com', 'email')
            ->type('bB2bB2', 'password')
            ->press('Login')
            ->see('These credentials do not match our records');
    }
}
