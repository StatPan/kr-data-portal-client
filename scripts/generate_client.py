import yaml
from jinja2 import Template

TEMPLATE = """
from typing import Any, Dict, Optional, Union
from .client import DataPortalClient
from .models.base import DataPortalResponse
from .models.{{ module_name }} import {{ models_list | join(', ') }}

class {{ class_name }}(DataPortalClient):
    \"\"\"{{ description }}
    
    Base URL: {{ base_url }}
    \"\"\"

    {% for service in services %}
    async def {{ service.name }}(
        self,
        {% for param in service.parameters if param.name != 'serviceKey' and param.name != 'resultType' %}
        {{ param.name }}: {{ param.type }} = {{ param.default if param.default is defined and param.default is not none else 'None' }},
        {% endfor %}
        **kwargs: Any
    ) -> DataPortalResponse[{{ service.model_name }}]:
        \"\"\"{{ service.description }}

        Data Update Policy:
        - Cycle: {{ service.update_policy.cycle }}
        - Timing: {{ service.update_policy.timing }}

        Args:
            {% for param in service.parameters if param.name != 'serviceKey' and param.name != 'resultType' %}
            {{ param.name }} ({{ param.type }}): {{ param.description or 'No description' }}
            {% endfor %}
            **kwargs: Additional request parameters.

        Returns:
            DataPortalResponse[{{ service.model_name }}]: The API response.
        \"\"\"
        params = {
            "resultType": "json",
            {% for param in service.parameters if param.name != 'serviceKey' and param.name != 'resultType' %}
            "{{ param.name }}": {{ param.name }},
            {% endfor %}
        }
        params.update(kwargs)
        
        data = await self._request(
            "{{ base_url }}{{ service.path }}",
            params={k: v for k, v in params.items() if v is not None}
        )
        return DataPortalResponse[{{ service.model_name }}].model_validate(data)

    {% endfor %}
"""

MODEL_TEMPLATE = """
from pydantic import BaseModel
from typing import Optional

{% for service in services %}
class {{ service.model_name }}(BaseModel):
    \"\"\"Model for {{ service.name }} item.\"\"\"
    # Note: In production, these fields should be mapped based on actual API response
    # For now, we use dynamic fields or common ones if known.
    # We'll define some common stock fields here.
    basDt: Optional[str] = None
    srtnCd: Optional[str] = None
    isinCd: Optional[str] = None
    itmsNm: Optional[str] = None
    mrktCtg: Optional[str] = None
    clpr: Optional[str] = None
    vs: Optional[str] = None
    fltRt: Optional[str] = None
    mkp: Optional[str] = None
    hipr: Optional[str] = None
    lopr: Optional[str] = None
    trqu: Optional[str] = None
    trPrc: Optional[str] = None
    lstgStCnt: Optional[str] = None
    mrktTotAmt: Optional[str] = None

{% endfor %}
"""


def generate():
    with open("specs/financial_services.yaml") as f:
        spec = yaml.safe_load(f)

    services = spec["services"]
    for s in services:
        # Simple name conversion: getStockPriceInfo -> StockPrice
        s["model_name"] = s["name"].replace("get", "")
        if not s["model_name"].endswith("Item"):
            s["model_name"] += "Item"

    module_name = "financial_services"
    models_list = [s["model_name"] for s in services]

    # Generate Models
    model_t = Template(MODEL_TEMPLATE)
    model_content = model_t.render(services=services)
    with open(f"src/kr_data_portal/models/{module_name}.py", "w") as f:
        f.write(model_content)

    # Generate Client
    client_t = Template(TEMPLATE)
    client_content = client_t.render(
        module_name=module_name,
        class_name="FinancialClient",
        description=spec["info"]["description"],
        base_url=spec["info"]["base_url"],
        services=services,
        models_list=models_list,
    )
    with open(f"src/kr_data_portal/{module_name}.py", "w") as f:
        f.write(client_content)


if __name__ == "__main__":
    generate()
