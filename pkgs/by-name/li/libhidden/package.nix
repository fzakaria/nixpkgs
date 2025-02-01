{ stdenv }:

stdenv.mkDerivation {
    name = "libhidden";
    version = "0.1";
    src = ./.;

    buildPhase = ''
      make
    '';

    installPhase = ''
      mkdir -p $out/lib
      cp *.so $out/lib
    '';
  }