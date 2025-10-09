# Copyright (c) Microsoft. All rights reserved.


from dataclasses import dataclass
from typing import Annotated, Any

from pydantic import BaseModel

from semantic_kernel.connectors.ai.open_ai import OpenAIEmbeddingPromptExecutionSettings
from semantic_kernel.data.vector import (
    VectorStoreField,
    vectorstoremodel,
    FieldTypes
)

###
# The data model used for this sample is based on the hotel data model from the Azure AI Search samples.
# When deploying a new index in Azure AI Search using the import wizard you can choose to deploy the 'hotel-samples'
# dataset, see here: https://learn.microsoft.com/en-us/azure/search/search-get-started-portal.
# This is the dataset used in this sample with some modifications.
# This model adds vectors for the 2 descriptions in English and French.
# Both are based on the 1536 dimensions of the OpenAI models.
# You can adjust this at creation time and then make the change below as well.
###


@vectorstoremodel
@dataclass
class EmployeeHandbookModel(BaseModel):
    id: Annotated[str, VectorStoreField(FieldTypes.KEY)]
    content: Annotated[str, VectorStoreField(FieldTypes.DATA)]
    title: Annotated[str, VectorStoreField(FieldTypes.DATA)]
    url: Annotated[str, VectorStoreField(FieldTypes.DATA)]
    filepath: Annotated[str, VectorStoreField(FieldTypes.DATA)]
    meta_json_string: Annotated[str, VectorStoreField(FieldTypes.DATA)]
    contentVector: Annotated[
        list[float] | None,
        VectorStoreField(
            dimensions=1536,
            field_type=FieldTypes.VECTOR
        ),
    ] = None

   