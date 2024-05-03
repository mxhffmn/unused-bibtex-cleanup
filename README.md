unused_bibtex_cleanup.py
========================

## Description

Deletes unreferenced entries from a bibtex file. References are searched in all files with the ending .tex in the given
folder. The tool also recognizes the citations of natbib. The behavior of the tool can be customized by a few parameters.

## Usage

Using the tool is pretty simple. Assuming we have a bibtex file called `my_bibtex_file.bib` with the following content

```
@ARTICLE{smit54,
	AUTHOR = {J. G. Smith and H. K. Weston},
	TITLE = {Nothing Particular in this Year's History},
	YEAR = {1954},
	JOURNAL = {J. Geophys. Res.},
	VOLUME = {2},
	PAGES = {14-15}
}

@BOOK{colu92,
	AUTHOR = {Christopher Columbus},
	TITLE = {How {I} Discovered {America}},
	YEAR = {1492},
	PUBLISHER = {Hispanic Press},
	ADDRESS = {Barcelona}
}

@ARTICLE{gree00,
	AUTHOR = {R. J. Green and U. P. Fred and W. P. Norbert},
	TITLE = {Things that Go Bump in the Night},
	YEAR = {1900},
	JOURNAL = {Psych. Today},
	VOLUME = {46},
	PAGES = {345-678}
}
```
and a folder, called `my_folder_with_tex_files`, that contains a file called `text.tex` with the content

```
This is my text where I am citing \cite{colu92} and \citet{smit54}.
```

then the command

```bash
unused_bibtex_cleanup.py my_bibtex_file.bib my_folder_with_tex_files
```

overwrites the given bibtex file with the following output:

```
%%%%%%%%%%%%%%%%%%%%%%%
%%% MODIFIED BIBTEX %%%
%%%%%%%%%%%%%%%%%%%%%%%

@ARTICLE{smit54,
    AUTHOR = "Smith, J. G. and Weston, H. K.",
    TITLE = "Nothing Particular in this Year's History",
    YEAR = "1954",
    JOURNAL = "J. Geophys. Res.",
    VOLUME = "2",
    PAGES = "14-15"
}

@BOOK{colu92,
    AUTHOR = "Columbus, Christopher",
    TITLE = "How {I} Discovered {America}",
    YEAR = "1492",
    PUBLISHER = "Hispanic Press",
    ADDRESS = "Barcelona"
}

%ARTICLE{gree00,
%    AUTHOR = "Green, R. J. and Fred, U. P. and Norbert, W. P.",
%    TITLE = "Things that Go Bump in the Night",
%    YEAR = "1900",
%    JOURNAL = "Psych. Today",
%    VOLUME = "46",
%    PAGES = "345-678"
%}
```

## Required Positional Parameters

| parameter  | description                                                                                                         |
|------------|---------------------------------------------------------------------------------------------------------------------|
| bib_file   | the path to the bibtex file. Can be absolute or relative.                                                           |
| tex_folder | the path to the folder of tex files to look through. The path is searched recursively. Can be absolute or relative. |


## Optional Parameters

| parameter       | description                                                                                                                                     |
|:----------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| `--no_comments` | if set, the unused entries will not remain in the output as comments.                                                                           |
| `--dry_run`     | if set, the tool will perform a dry-run, only printing its actions without actually performing them. This is useful for testing and debugging.  |

## License

MIT
