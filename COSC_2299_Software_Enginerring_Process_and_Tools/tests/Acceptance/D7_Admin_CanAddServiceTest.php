<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class D7_Admin_CanAddServiceTest extends TestCase
{
    /**
     *
     * @return void
     */
    public function testCanAddService()
    {
        $this->visit('/login')
            ->type('admin@example.com', 'email')
            ->type('Admin1', 'password')
            ->press('Login')
            ->see('Admin Menu')
            ->click('Add Service')
            ->see('Add Service')
            ->type('Assisted Suicide', 'name')
            ->type('60', 'duration_in_minutes')
            ->press('Add Service')
            ->see('Assisted Suicide was added as a service');
    }
}
