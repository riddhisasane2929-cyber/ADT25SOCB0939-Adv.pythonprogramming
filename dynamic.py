from functools import wraps
from datetime import datetime


# ============================================================
# Formatting Decorators
# ============================================================

def uppercase(func):
    """Convert generated report text to uppercase."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def add_header(title):
    """Add a formatted header to the report."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            report = func(*args, **kwargs)
            header = f"{'=' * 60}\n{title.center(60)}\n{'=' * 60}\n"
            return header + report
        return wrapper
    return decorator


def add_footer(text="End of Report"):
    """Add a footer to the report."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            report = func(*args, **kwargs)
            return f"{report}\n{'-' * 60}\n{text}\n"
        return wrapper
    return decorator


def add_timestamp(func):
    """Add generation time to the report."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        report = func(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Generated: {timestamp}\n\n{report}"
    return wrapper


def bullet_points(func):
    """Convert list-like report content into bullet points."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        report = func(*args, **kwargs)

        lines = report.splitlines()
        formatted = []

        for line in lines:
            if line.strip():
                formatted.append(f"• {line}")
            else:
                formatted.append(line)

        return "\n".join(formatted)

    return wrapper


# ============================================================
# Report Template
# ============================================================

class ReportTemplate:
    """
    Represents a user-defined report template.
    """

    def __init__(self, name, template):
        self.name = name
        self.template = template

    def render(self, **data):
        """Render the template using supplied data."""
        try:
            return self.template.format(**data)
        except KeyError as exc:
            raise ValueError(
                f"Missing template variable: {exc.args[0]}"
            ) from exc

    def __str__(self):
        return f"ReportTemplate(name='{self.name}')"


# ============================================================
# Dynamic Report Generator
# ============================================================

class ReportGenerator:

    _templates = {}

    def __init__(self, template_name, **data):
        if template_name not in self._templates:
            raise ValueError(
                f"Template '{template_name}' does not exist."
            )

        self.template_name = template_name
        self.data = data
        self.formatters = []

    # --------------------------------------------------------
    # Class Method
    # --------------------------------------------------------

    @classmethod
    def register_template(cls, name, template):
        """
        Register a new report template.

        Example:
            ReportGenerator.register_template(
                "sales",
                "Sales Report\\nRevenue: ₹{revenue}"
            )
        """
        cls._templates[name] = ReportTemplate(name, template)
        return cls

    @classmethod
    def create(cls, template_name, **data):
        """
        Factory-style class method for creating reports.
        """
        return cls(template_name, **data)

    @classmethod
    def list_templates(cls):
        """Return all available template names."""
        return list(cls._templates.keys())

    # --------------------------------------------------------
    # Dynamic Formatting
    # --------------------------------------------------------

    def add_formatter(self, formatter):
        """
        Add a formatter dynamically.

        The formatter must be a function that accepts
        report text and returns modified report text.
        """
        self.formatters.append(formatter)
        return self

    def generate(self):
        """Generate and format the report."""

        template = self._templates[self.template_name]

        report = template.render(**self.data)

        # Apply dynamically registered formatters
        for formatter in self.formatters:
            report = formatter(report)

        return report

    # --------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------

    def __str__(self):
        """Allows print(report)."""
        return self.generate()

    def __call__(self):
        """Allows report() to generate the report."""
        return self.generate()

    def __getitem__(self, key):
        """Allows report['revenue']."""
        return self.data[key]

    def __setitem__(self, key, value):
        """Allows report['revenue'] = 50000."""
        self.data[key] = value

    def __iter__(self):
        """Iterate over report data."""
        return iter(self.data.items())

    def __len__(self):
        """Number of data fields."""
        return len(self.data)

    def __repr__(self):
        return (
            f"ReportGenerator("
            f"template='{self.template_name}', "
            f"fields={len(self.data)})"
        )


# ============================================================
# Example Custom Formatter
# ============================================================

def emphasize_revenue(report):
    """Example user-defined formatter."""
    return report.replace("Revenue:", ">>> Revenue:")


# ============================================================
# Register User Templates
# ============================================================

ReportGenerator.register_template(
    "sales",
    """
Sales Report

Salesperson : {employee}
Department  : {department}
Revenue     : ₹{revenue}
Units Sold  : {units}
Performance : {performance}
"""
)

ReportGenerator.register_template(
    "employee",
    """
Employee Report

Name        : {name}
Department  : {department}
Experience  : {experience} years
Rating      : {rating}/5
"""
)


# ============================================================
# Create a Report
# ============================================================

sales_report = ReportGenerator.create(
    "sales",
    employee="Rahul",
    department="Electronics",
    revenue=125000,
    units=450,
    performance="Excellent"
)


# Dynamically add formatting
sales_report \
    .add_formatter(emphasize_revenue) \
    .add_formatter(str.strip)


print(sales_report)