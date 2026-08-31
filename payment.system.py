from functools import wraps
from datetime import datetime


# =========================================================
# DECORATORS
# =========================================================

def add_header(title):
    """Decorator to add a header to the report."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            report = func(*args, **kwargs)

            header = (
                "=" * 60 + "\n"
                + title.center(60)
                + "\n"
                + "=" * 60 + "\n"
            )

            return header + report

        return wrapper

    return decorator


def add_footer(text="END OF REPORT"):
    """Decorator to add a footer."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            report = func(*args, **kwargs)

            footer = (
                "\n"
                + "-" * 60
                + "\n"
                + text.center(60)
                + "\n"
            )

            return report + footer

        return wrapper

    return decorator


def add_timestamp(func):
    """Decorator to add report generation time."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        report = func(*args, **kwargs)

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        return f"Generated On: {timestamp}\n\n{report}"

    return wrapper


def uppercase(func):
    """Decorator to convert the report into uppercase."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()

    return wrapper


# =========================================================
# REPORT TEMPLATE CLASS
# =========================================================

class ReportTemplate:

    def __init__(self, name, template):
        self.name = name
        self.template = template

    def render(self, **data):
        """Replace template placeholders with actual data."""

        try:
            return self.template.format(**data)

        except KeyError as error:
            raise ValueError(
                f"Missing data field: {error.args[0]}"
            )

    def __str__(self):
        return f"Template: {self.name}"


# =========================================================
# REPORT GENERATOR
# =========================================================

class ReportGenerator:

    # Class-level dictionary containing all templates
    templates = {}

    def __init__(self, template_name, **data):

        if template_name not in ReportGenerator.templates:
            raise ValueError(
                f"Template '{template_name}' does not exist."
            )

        self.template_name = template_name
        self.data = data
        self.formatters = []

    # -----------------------------------------------------
    # CLASS METHODS
    # -----------------------------------------------------

    @classmethod
    def register_template(cls, name, template):
        """Register a new report template."""

        cls.templates[name] = ReportTemplate(
            name,
            template
        )

    @classmethod
    def create_report(cls, template_name, **data):
        """Create a report using a registered template."""

        return cls(template_name, **data)

    @classmethod
    def show_templates(cls):
        """Display all available templates."""

        print("\nAvailable Templates:")

        for name in cls.templates:
            print(f"- {name}")

    # -----------------------------------------------------
    # FORMATTER
    # -----------------------------------------------------

    def add_formatter(self, formatter):
        """Add a formatter dynamically."""

        self.formatters.append(formatter)

        return self

    # -----------------------------------------------------
    # GENERATE REPORT
    # -----------------------------------------------------

    def generate(self):

        template = self.templates[self.template_name]

        report = template.render(**self.data)

        # Apply all dynamically added formatters
        for formatter in self.formatters:
            report = formatter(report)

        return report

    # =====================================================
    # MAGIC METHODS
    # =====================================================

    def __str__(self):
        """Called when print(report) is used."""

        return self.generate()

    def __call__(self):
        """Allows report() to generate the report."""

        return self.generate()

    def __getitem__(self, key):
        """Allows report['name']."""

        return self.data[key]

    def __setitem__(self, key, value):
        """Allows report['name'] = value."""

        self.data[key] = value

    def __len__(self):
        """Returns number of data fields."""

        return len(self.data)

    def __iter__(self):
        """Allows iteration over report data."""

        return iter(self.data.items())

    def __repr__(self):
        return (
            f"ReportGenerator("
            f"template='{self.template_name}', "
            f"fields={len(self.data)})"
        )


# =========================================================
# CUSTOM FORMATTERS
# =========================================================

def emphasize_revenue(report):
    """Custom formatter."""

    return report.replace(
        "Revenue",
        ">>> Revenue"
    )


def remove_empty_lines(report):
    """Remove unnecessary empty lines."""

    lines = report.splitlines()

    return "\n".join(
        line for line in lines
        if line.strip()
    )


# =========================================================
# REGISTER TEMPLATES
# =========================================================

ReportGenerator.register_template(
    "sales",
    """
Employee   : {employee}
Department : {department}
Revenue    : ₹{revenue}
Units Sold : {units}
Performance: {performance}
"""
)


ReportGenerator.register_template(
    "employee",
    """
Name       : {name}
Department : {department}
Experience : {experience} years
Rating     : {rating}/5
"""
)


# =========================================================
# DISPLAY AVAILABLE TEMPLATES
# =========================================================

ReportGenerator.show_templates()


# =========================================================
# CREATE SALES REPORT
# =========================================================

sales_report = ReportGenerator.create_report(
    "sales",
    employee="Rahul",
    department="Electronics",
    revenue=150000,
    units=500,
    performance="Excellent"
)


# Dynamically apply formatters
sales_report.add_formatter(emphasize_revenue)
sales_report.add_formatter(remove_empty_lines)


print("\nSALES REPORT")
print(sales_report)


# =========================================================
# MAGIC METHOD EXAMPLES
# =========================================================

print("\nMAGIC METHOD EXAMPLES")

# __getitem__
print("Employee:", sales_report["employee"])

# __setitem__
sales_report["revenue"] = 175000

print("Updated Revenue:", sales_report["revenue"])

# __len__
print("Number of fields:", len(sales_report))

# __iter__
print("\nReport Data:")

for key, value in sales_report:
    print(f"{key}: {value}")

# __call__
print("\nGenerated using report():")
print(sales_report())