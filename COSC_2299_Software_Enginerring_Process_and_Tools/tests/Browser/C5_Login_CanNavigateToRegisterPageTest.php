<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class C5_Login_CanNavigateToRegisterPageTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testC5_Login_CanNavigateToRegisterPage()
    {
        $this->browse(function ($browser) {
            $browser->visit('/login')
                    ->type('email', 'bill@microsoft.com')
                    ->clickLink('Register')
                    ->assertPathIs('/register');
        });
    }
}
