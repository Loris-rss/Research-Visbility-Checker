from ._misc import markdown_title, move_column_first
from ._hal import get_hal_researcher_data, id_author, base_link
from ._scopus import Scopus_Researcher
from ._tx_recoupement import TxRecoupement, compare_publication_databases, compare_all_databases, suggest_column_mapping, create_id_column
from ._wos import CheckResearcherInPaper, action_suggeree
from ._orcid import Orcid_Researcher

__all__ = ["get_hal_researcher_data",
        "markdown_title",
        "Scopus_Researcher",
        "move_column_first",
        "TxRecoupement",
        "CheckResearcherInPaper",
        "action_suggeree",
        "Orcid_Researcher",
        "compare_publication_databases",
        "compare_all_databases",
        "suggest_column_mapping",
        "id_author",
        "base_link",
        "create_id_column",
]