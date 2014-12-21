#!/bin/sh
VERSION=1.10.5
svn export --username guest --password "" http://subclipse.tigris.org/svn/subclipse/tags/subclipse/$VERSION/subclipse subclipse-$VERSION

#those sources are missing from the plugin, so copy them back!
svn export --username guest --password "" http://subclipse.tigris.org/svn/subclipse/tags/subclipse/$VERSION/svnClientAdapter/src/main adapter-$VERSION/
cp -r adapter-$VERSION/* subclipse-$VERSION/org.tigris.subversion.clientadapter/src

rm -rf ./subclipse-$VERSION/org.tigris.subversion.clientadapter.javahl.win*
tar -caf subclipse-$VERSION.tar.xz subclipse-$VERSION
