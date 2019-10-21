<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class C4_Login_CanNavigateToForgotYourPasswordPageTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testC4_Login_CanNavigateToForgetYourPasswordPage()
    {
        $this->browse(function ($browser) {
            $browser->visit('/login')
                    ->type('email', 'bill@microsoft.com')
                    ->clickLink('Forgot Your Password?')
                    ->assertPathIs('/password/reset');
        });
    }
}
