<?php

require __DIR__ . '/vendor/autoload.php';

use Doctrine\Inflector\InflectorFactory;

$inflector = InflectorFactory::create()->build();
echo $inflector->pluralize($argv[1]);