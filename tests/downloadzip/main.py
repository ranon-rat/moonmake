import moonmake as mmake


zip_url="https://www.sqlite.org/2025/sqlite-amalgamation-3490100.zip"
mmake.download_dependency(zip_url,"sqlite",".moonmake/dependencies")

