<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class C1_Login_CanSeeLoginPageTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testC1_Login_CanSeeLoginPage()
    {
        $this->browse(function ($browser) {
            $browser->visit('/login')
                    ->assertSee('Login');
        });
    }
}
