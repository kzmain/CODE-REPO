<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class C2_Login_CanLoginTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testC2_Login_CanLogin()
    {
        $this->browse(function ($browser) {
            $browser->visit('/login')
                    ->type('email', 'bill@microsoft.com')
                    ->type('password', 'aA1aA1')
                    ->press('Login')
                    ->assertPathIs('/home');
        });
    }
}
