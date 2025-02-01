{
  libhidden,
  stdenv,
}:
stdenv.mkDerivation {
  name = "hidden";
  version = "0.1";
  src = ./.;

  buildInputs = [libhidden];

  buildPhase = ''
    make
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp hidden $out/bin
    cp public $out/bin
  '';
}
