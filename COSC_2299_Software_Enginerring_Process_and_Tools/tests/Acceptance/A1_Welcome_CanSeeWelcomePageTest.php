<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class A1_Welcome_CanSeeWelcomePageTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function testCanSeeWelcomePage()
    {
        $this->visit('/')
            ->see('Logo');
    }
}
