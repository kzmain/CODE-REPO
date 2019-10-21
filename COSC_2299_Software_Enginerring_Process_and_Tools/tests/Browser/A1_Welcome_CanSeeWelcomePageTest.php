<?php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;

class A1_Welcome_CanSeeWelcomePageTest extends DuskTestCase
{
    /**
     *
     * @return void
     */
    public function testA1_Welcome_CanSeeWelcomePageTest()
    {
        $this->browse(function ($browser) {
            $browser->visit('/')
                    ->assertSee('Logo');
        });
    }
}
