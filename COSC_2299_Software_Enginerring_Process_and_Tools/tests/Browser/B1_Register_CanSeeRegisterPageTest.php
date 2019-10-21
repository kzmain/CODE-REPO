<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class B1_Register_CanSeeRegisterPageTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testB1_Register_CanSeeRegisterPage()
    {
        $this->browse(function ($browser) {
            $browser->visit('/register')
                    ->assertSee('Register');
        });
    }
}
