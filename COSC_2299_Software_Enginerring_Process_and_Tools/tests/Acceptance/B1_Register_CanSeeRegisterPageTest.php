<?php

namespace Tests\Acceptance;

use Tests\TestCase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

class B1_Register_CanSeeRegisterPageTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function testCanSeeRegisterPageTest()
    {
        $this->visit('/register')
            ->see('Register');
    }
}
