# AWS Layers

- [docs](docs)

~~~
#!/bin/bash

pushd .
cd layers
zip -vr  -9 ../build/layers.zip python -x '*/__pycache__/*'
popd
~~~