for ((i=0; i<10;++i))do
    echo "start $i client_pages"
    python new_client_pages.py xdunews&
done
