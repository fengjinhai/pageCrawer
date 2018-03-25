for ((i=0; i<20;++i))do
    echo "start $i client_pages"
    python client_pages.py xdunews&
done
