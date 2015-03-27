SPECFILE := python-gccjit.spec
VERSION := $(shell rpm -q --qf "%{VERSION}\n" --specfile $(SPECFILE)| head -1)
RELEASE := $(shell rpm -q --qf "%{RELEASE}\n" --specfile $(SPECFILE)| head -1)

srpm:
	rpmbuild -bs $(SPECFILE) --define="_sourcedir $(shell pwd)"

rpm:
	rpmbuild -ba $(SPECFILE) --define="_sourcedir $(shell pwd)"

# Given an rpmbuild, skip ahead to the %install phase
rpm-skip-to-install:
	rpmbuild --short-circuit -bi $(SPECFILE) --define="_sourcedir $(shell pwd)"

# Upload to a location that COPR can read from
upload-srpm:
	scp \
	  ~/rpmbuild/SRPMS/python-gccjit-$(VERSION)-$(RELEASE).src.rpm \
	  dmalcolm@fedorapeople.org:public_html/gcc/libgccjit-srpms

local-mock-fedora-rawhide-x86_64:
	mock --rebuild \
	  ~/rpmbuild/SRPMS/python-gccjit-$(VERSION)-$(RELEASE).src.rpm \
	  -r fedora-rawhide-x86_64

local-mock-fedora-20-x86_64:
	mock --rebuild \
	  ~/rpmbuild/SRPMS/python-gccjit-$(VERSION)-$(RELEASE).src.rpm \
	  -r fedora-20-x86_64

local-mock-epel-6-x86_64:
	mock --rebuild \
	  ~/rpmbuild/SRPMS/python-gccjit-$(VERSION)-$(RELEASE).src.rpm \
	  -r epel-6-x86_64

local-mock-epel-6-i386:
	mock --rebuild \
	  ~/rpmbuild/SRPMS/python-gccjit-$(VERSION)-$(RELEASE).src.rpm \
	  -r epel-6-i386

tarball:
	cp ~/coding/gcc-python/pygccjit-clean/dist/gccjit-$(VERSION).tar.gz .
