# AWS Layers

- [docs](docs)

~~~
#!/bin/bash

pushd .
cd layers
zip -vr  -9 ../build/layers.zip python -x '*/__pycache__/*'
popd
~~~


## Notice

This product includes software developed at:

* hdknr
* Lafoglia,Inc

Copyright 2020  Hideki Nara

Brand names include, but are not limited to:

* py-layers

this software without prior written permission of Hideki Nara.

For license information, please read the LICENSE file.


## poetry

~~~
% poetry add -D pysen -E lint
~~~
