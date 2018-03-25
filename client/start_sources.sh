for ((i=0; i<10;++i))do
    echo "start $i client_sources"
    nohup python client_sources.py jinhai&
done
