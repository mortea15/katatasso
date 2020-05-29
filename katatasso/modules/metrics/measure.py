import sys
from datetime import datetime

from katatasso.helpers.const import categories
from katatasso.helpers.logger import rootLogger as logger

try:
    from sklearn.metrics import classification_report, plot_confusion_matrix
    from sklearn.model_selection import cross_val_score
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    logger.critical(f'Module `{e.name}` not found. Please install before proceeding.')
    sys.exit(2)


def evaluate(model, X, y):
    num_validations = 5

    accuracy = cross_val_score(model, X, y, scoring='accuracy', cv=num_validations)
    print(f'Accuracy: {str(round(100*accuracy.mean(), 2))}%')

    f1 = cross_val_score(model, X, y, scoring='f1_weighted', cv=num_validations)
    print(f'F1: {str(round(100*f1.mean(), 2))}%')

    precision = cross_val_score(model, X, y, scoring='precision_weighted', cv=num_validations)
    print(f'Precision: {str(round(100*precision.mean(), 2))}%')

    recall = cross_val_score(model, X, y, scoring='recall_weighted', cv=num_validations)
    print(f'Recall: {str(round(100*recall.mean(), 2))}%')


def performance_report(y_test, y_pred):
    try:
        print(classification_report(y_test, y_pred, target_names=categories, zero_division=0))
    except ValueError as e:
        logger.critical(f'Classification report: Invalid param `target_names`.')
        logger.error(e)
        print(classification_report(y_test, y_pred, zero_division=0))


def plot_confusion_mat(model, x_test, y_test):
    plot_confusion_matrix(model, x_test, y_test, display_labels=categories, values_format='')
    now = datetime.now().isoformat()
    plt.savefig(f'confusion-matrix_{now}.png')
    try:
        plt.show()
    except:
        pass
