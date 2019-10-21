<?php

namespace Tests\Unit;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTransactions;

use App\Service;

class ServiceTest extends TestCase
{
    public function testValidInput()
    {
        $input = array(
            'name' => 'homy',
            'duration_in_minutes' => '60',
        );
        $validator = Service::validator($input);
        $this->assertTrue($validator->passes());
    }

    public function testEmptyInput()
    {
        $input = array();
        $validator = Service::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidName()
    {
        $input = array(
            'name' => 'saucqw90dj10dnfoasklmdkm309jd0923j09d2398fh349f8298fqw0jd09qwjd09qwjd90j1802jcd 1j98dcn09jd09jn09qejc0912jm09ej0192cjn981ce8jn9cj109ecj9jec0912jec9012jec1n90ejc09jecn0912je90cj10ejoiqwjdj90jd9012jwqd3r1j98dcn09jd09jn09qejc0912jm09ej0192cjn981ce8jn9cj109ecj9jec0912jec9012jec1n90ejc09jecn0912je90cj10ejoiqwjdj90jd9012jwqd3r',
            'duration_in_minutes' => '60',
        );
        $validator = Service::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testInvalidDuration_In_Minutes()
    {
        $input = array(
            'name' => 'homy',
            'duration_in_minutes' => 'a',
        );
        $validator = Service::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testEmptyName()
    {
        $input = array(
            'name' => '',
            'duration_in_minutes' => '60',
        );
        $validator = Service::validator($input);
        $this->assertTrue($validator->fails());
    }

    public function testEmptyDuration_In_Minutes()
    {
        $input = array(
            'name' => 'homy',
            'duration_in_minutes' => '',
        );
        $validator = Service::validator($input);
        $this->assertTrue($validator->fails());
    }
  }
