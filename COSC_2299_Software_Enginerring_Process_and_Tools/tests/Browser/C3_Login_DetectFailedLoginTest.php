<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class C3_Login_DetectFailedLoginTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testC3_Login_DetectFailedLogin()
    {
        $this->browse(function ($browser) {
            $browser->visit('/login')
                    ->type('email', 'bill@microsoft.com')
                    ->type('password', 'bB2bB2')
                    ->press('Login')
                    ->assertSee('These credentials do not match our records');
        });
    }
}
