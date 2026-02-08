from pathlib import Path

import jinja2
import yaml


# StatPan's dart-api-client inspired generator stub
def generate():
    spec_path = Path("specs/financial_services.yaml")
    with spec_path.open(encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    template_str = """
    {% for name, details in endpoints.items() %}
    async def {{ name }}(self, **kwargs) -> ApiResponse:
        \"\"\"
        {{ details.description }}
        
        Update Policy: {{ update_policy.refresh_cycle }}
        Update Timing: {{ update_policy.update_timing }}
        \"\"\"
        return await self._get("{{ details.path }}", kwargs)
    {% endfor %}
    """

    template = jinja2.Template(template_str)
    rendered = template.render(endpoints=spec["endpoints"], update_policy=spec["update_policy"])

    print("🌿 Generated Methods based on YAML spec:")
    print(rendered)


if __name__ == "__main__":
    # In a real scenario, this would write to client_generated.py
    print("Simulating code generation from YAML...")
    # generate()
